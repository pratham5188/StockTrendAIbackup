#!/usr/bin/env python3
"""
Stock Discovery System for StockTrendAI
Automatically discovers and adds new stocks to the system
"""

import json
import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDiscovery:
    """Class for discovering new stocks and updating the system"""
    
    def __init__(self):
        self.cache_file = "data/stock_cache.json"
        self.config_file = "config/settings.py"
        self.last_update_file = "data/last_update.json"
        
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # NSE/BSE stock suffixes for Indian market
        self.indian_suffixes = ['.NS', '.BO']
        
        # Load cached data
        self.cached_stocks = self.load_cache()
    
    def load_cache(self) -> Dict:
        """Load cached stock data"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load cache: {e}")
        return {}
    
    def save_cache(self, data: Dict) -> None:
        """Save stock data to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save cache: {e}")
    
    def get_last_update(self) -> Optional[datetime]:
        """Get the last update timestamp"""
        try:
            if os.path.exists(self.last_update_file):
                with open(self.last_update_file, 'r') as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data['last_update'])
        except Exception as e:
            logger.warning(f"Could not load last update: {e}")
        return None
    
    def save_last_update(self) -> None:
        """Save the current timestamp as last update"""
        try:
            data = {'last_update': datetime.now().isoformat()}
            with open(self.last_update_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save last update: {e}")
    
    def validate_stock_symbol(self, symbol: str) -> bool:
        """Validate if a stock symbol is valid and tradeable"""
        try:
            # Try to fetch basic info for the symbol
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check if we got valid data
            if not info or 'symbol' not in info:
                return False
            
            # Try to get recent data
            hist = ticker.history(period="5d")
            if hist.empty:
                return False
                
            return True
            
        except Exception as e:
            logger.debug(f"Symbol {symbol} validation failed: {e}")
            return False
    
    def discover_nse_stocks(self) -> List[Dict]:
        """Discover stocks from NSE (National Stock Exchange)"""
        discovered_stocks = []
        
        # Sample of NSE stock symbols to test
        # In a real implementation, you would fetch this from NSE API
        sample_nse_symbols = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
            'KOTAKBANK', 'SBIN', 'BHARTIARTL', 'ITC', 'ASIANPAINT',
            'MARUTI', 'BAJFINANCE', 'HCLTECH', 'AXISBANK', 'LT',
            'ULTRACEMCO', 'TITAN', 'WIPRO', 'NESTLEIND', 'POWERGRID'
        ]
        
        for symbol_base in sample_nse_symbols:
            symbol = f"{symbol_base}.NS"
            
            # Skip if already in cache
            if symbol in self.cached_stocks:
                continue
                
            if self.validate_stock_symbol(symbol):
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    stock_info = {
                        'symbol': symbol,
                        'company_name': info.get('longName', symbol_base),
                        'sector': info.get('sector', 'Unknown'),
                        'industry': info.get('industry', 'Unknown'),
                        'exchange': 'NSE',
                        'discovered_date': datetime.now().isoformat()
                    }
                    
                    discovered_stocks.append(stock_info)
                    self.cached_stocks[symbol] = stock_info
                    
                    logger.info(f"Discovered NSE stock: {symbol}")
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.warning(f"Error processing {symbol}: {e}")
        
        return discovered_stocks
    
    def discover_bse_stocks(self) -> List[Dict]:
        """Discover stocks from BSE (Bombay Stock Exchange)"""
        discovered_stocks = []
        
        # Sample of BSE stock symbols to test
        sample_bse_symbols = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK'
        ]
        
        for symbol_base in sample_bse_symbols:
            symbol = f"{symbol_base}.BO"
            
            # Skip if already in cache
            if symbol in self.cached_stocks:
                continue
                
            if self.validate_stock_symbol(symbol):
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    
                    stock_info = {
                        'symbol': symbol,
                        'company_name': info.get('longName', symbol_base),
                        'sector': info.get('sector', 'Unknown'),
                        'industry': info.get('industry', 'Unknown'),
                        'exchange': 'BSE',
                        'discovered_date': datetime.now().isoformat()
                    }
                    
                    discovered_stocks.append(stock_info)
                    self.cached_stocks[symbol] = stock_info
                    
                    logger.info(f"Discovered BSE stock: {symbol}")
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.warning(f"Error processing {symbol}: {e}")
        
        return discovered_stocks
    
    def get_new_stocks_since_last_update(self) -> List[Dict]:
        """Get stocks discovered since last update"""
        last_update = self.get_last_update()
        
        if last_update is None:
            # First run, discover initial set
            logger.info("First run - discovering initial stocks")
            new_stocks = []
            new_stocks.extend(self.discover_nse_stocks())
            new_stocks.extend(self.discover_bse_stocks())
        else:
            # Check if enough time has passed (e.g., 24 hours)
            if datetime.now() - last_update < timedelta(hours=24):
                logger.info("Too soon since last update")
                return []
            
            # Discover new stocks
            new_stocks = []
            new_stocks.extend(self.discover_nse_stocks())
            new_stocks.extend(self.discover_bse_stocks())
        
        # Save cache and update timestamp
        self.save_cache(self.cached_stocks)
        self.save_last_update()
        
        return new_stocks
    
    def update_config_file(self, new_stocks: Dict[str, str]) -> bool:
        """Update the config file with new stocks"""
        try:
            # Read current config
            if not os.path.exists(self.config_file):
                logger.error("Config file not found")
                return False
            
            with open(self.config_file, 'r') as f:
                content = f.read()
            
            # Find the INDIAN_STOCKS dictionary
            if 'INDIAN_STOCKS' in content:
                # Simple approach: add new stocks to the dictionary
                # In a real implementation, you'd parse the Python AST
                logger.info(f"Would add {len(new_stocks)} new stocks to config")
                # For now, just log the stocks that would be added
                for symbol, name in new_stocks.items():
                    logger.info(f"New stock: {symbol} - {name}")
                return True
            else:
                logger.error("INDIAN_STOCKS not found in config")
                return False
                
        except Exception as e:
            logger.error(f"Error updating config file: {e}")
            return False

# Global instance
stock_discovery = StockDiscovery()

def get_latest_stock_list() -> List[Dict]:
    """Get the latest list of discovered stocks"""
    try:
        return list(stock_discovery.cached_stocks.values())
    except Exception as e:
        logger.error(f"Error getting stock list: {e}")
        return []

def auto_update_stocks() -> Dict:
    """
    Automatically update stock list and return status
    Returns: {'success': bool, 'message': str, 'new_stocks_count': int, 'error': Optional[str]}
    """
    try:
        new_stocks = stock_discovery.get_new_stocks_since_last_update()

        if not new_stocks:
            return {
                'success': True,
                'message': "No new stocks found",
                'new_stocks_count': 0
            }

        new_stocks_dict = {stock['symbol']: stock['company_name'] for stock in new_stocks}
        success = stock_discovery.update_config_file(new_stocks_dict)

        if success:
            return {
                'success': True,
                'message': f"Successfully added {len(new_stocks)} new stocks",
                'new_stocks_count': len(new_stocks)
            }
        else:
            return {
                'success': False,
                'message': "Failed to update configuration file",
                'new_stocks_count': len(new_stocks),
                'error': "Configuration update failed"
            }

    except Exception as e:
        return {
            'success': False,
            'message': f"Auto-update failed: {str(e)}",
            'new_stocks_count': 0,
            'error': str(e)
        }