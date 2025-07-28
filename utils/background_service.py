#!/usr/bin/env python3
"""
Background Service for StockTrendAI
Manages automatic stock discovery and notifications
"""

import threading
import time
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Safe import of schedule with fallback
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: schedule module not available: {e}")
    print("Background scheduling will be disabled. Install with: pip install schedule")
    SCHEDULE_AVAILABLE = False
    schedule = None

from .stock_discovery import auto_update_stocks

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundStockService:
    """Background service for automatic stock discovery and updates"""

    def __init__(self):
        self.is_running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.last_update = None
        self.update_notifications = []
        self.notification_file = "data/notifications.json"

        os.makedirs("data", exist_ok=True)
        self.load_notifications()

    def load_notifications(self):
        """Load notifications from file"""
        try:
            if os.path.exists(self.notification_file):
                with open(self.notification_file, 'r') as f:
                    data = json.load(f)
                    self.update_notifications = data.get('notifications', [])
        except Exception as e:
            logger.warning(f"Could not load notifications: {e}")
            self.update_notifications = []

    def save_notifications(self):
        """Save notifications to file"""
        try:
            data = {
                'notifications': self.update_notifications,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.notification_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save notifications: {e}")

    def add_notification(self, message: str, notification_type: str = "info"):
        """Add a new notification"""
        notification = {
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        self.update_notifications.append(notification)
        self.save_notifications()
        logger.info(f"Added notification: {message}")

    def get_unread_notifications(self) -> List[Dict]:
        """Get all unread notifications"""
        return [n for n in self.update_notifications if not n.get('read', False)]

    def mark_notifications_read(self):
        """Mark all notifications as read"""
        for notification in self.update_notifications:
            notification['read'] = True
        self.save_notifications()

    def clear_old_notifications(self, days_old: int = 7):
        """Clear notifications older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        self.update_notifications = [
            n for n in self.update_notifications 
            if datetime.fromisoformat(n['timestamp']) > cutoff_date
        ]
        self.save_notifications()

    def check_for_new_stocks(self):
        """Check for new stocks and update if found"""
        try:
            logger.info("Checking for new stocks...")
            result = auto_update_stocks()
            
            if result['success']:
                if result['new_stocks_count'] > 0:
                    message = f"🎉 Discovered {result['new_stocks_count']} new stocks! {result['message']}"
                    self.add_notification(message, "success")
                    logger.info(message)
                else:
                    logger.info("No new stocks found")
            else:
                message = f"⚠️ Stock discovery failed: {result['message']}"
                self.add_notification(message, "warning")
                logger.warning(message)
                
            self.last_update = datetime.now()
            
        except Exception as e:
            error_message = f"❌ Error in stock discovery: {str(e)}"
            self.add_notification(error_message, "error")
            logger.error(error_message)

    def run_scheduled_tasks(self):
        """Run scheduled background tasks"""
        if not SCHEDULE_AVAILABLE:
            logger.warning("Schedule module not available - background scheduling disabled")
            self.add_notification("⚠️ Background scheduling disabled - schedule module not found", "warning")
            return
        
        # Schedule stock discovery to run every 24 hours
        schedule.every(24).hours.do(self.check_for_new_stocks)
        
        # Schedule notification cleanup every week
        schedule.every().week.do(lambda: self.clear_old_notifications(7))
        
        logger.info("Background service started")
        self.add_notification("🚀 Background stock discovery service started", "info")
        
        while not self.stop_event.is_set():
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in background service: {e}")
                time.sleep(300)  # Wait 5 minutes on error

    def start(self):
        """Start the background service"""
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.run_scheduled_tasks, daemon=True)
            self.thread.start()
            logger.info("Background stock service started successfully")
            return True
        return False

    def stop(self):
        """Stop the background service"""
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.thread:
                self.thread.join(timeout=5)
            logger.info("Background service stopped")
            return True
        return False

    def get_status(self) -> Dict:
        """Get service status"""
        return {
            'is_running': self.is_running,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'unread_notifications': len(self.get_unread_notifications()),
            'total_notifications': len(self.update_notifications)
        }

# Global service instance
_background_service = None

def get_background_service() -> BackgroundStockService:
    """Get the global background service instance"""
    global _background_service
    if _background_service is None:
        _background_service = BackgroundStockService()
        _background_service.start()
    return _background_service

def get_service_status() -> Dict:
    """Get the status of the background service"""
    service = get_background_service()
    return service.get_status()

def get_notifications() -> List[Dict]:
    """Get all notifications from the background service"""
    service = get_background_service()
    return service.get_unread_notifications()

def mark_notifications_read():
    """Mark all notifications as read"""
    service = get_background_service()
    service.mark_notifications_read()

def trigger_stock_discovery():
    """Manually trigger stock discovery"""
    service = get_background_service()
    service.check_for_new_stocks()
    return "Stock discovery triggered manually"

# Auto-start the service when module is imported
try:
    get_background_service()
except Exception as e:
    logger.error(f"Failed to start background service: {e}")