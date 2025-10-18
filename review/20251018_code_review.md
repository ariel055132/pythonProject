# Code Review: Taiwan Stock Info Project (SOLID Principles Focus)
**Date:** October 18, 2025  
**Reviewer:** Senior Software Engineer  
**Project:** pythonProject - Taiwan Stock Information Fetcher  
**Focus:** SOLID Principles Compliance + General Code Quality

## Executive Summary

This code review analyzes a Python project that fetches Taiwan stock market data from the FinMind API and saves it to CSV files. The analysis focuses on SOLID principles compliance along with security, performance, code quality, architecture, and testing concerns.

## SOLID Principles Violations Analysis

### 🔴 **Single Responsibility Principle (SRP) Violations**

#### Violation 1: TaiwanStockInfo Class Mixed Concerns
**File:** `info/TaiwanStockInfo.py` (Lines 15-35)
```python
class TaiwanStockInfo:
    def __init__(self):
        self.base_url = 'https://api.finmindtrade.com/api/v4/data'

    def get_stock_deal_info(self, stock_id, start_date, end_date=None) -> List[Dict]:
        # ... date logic ...
        parameter = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        data = request_get(self.base_url, parameter)
        return data
```
**Problem:** The class handles both business logic (date defaulting) and API communication concerns.

**Solution:** Separate responsibilities:
```python
# Domain logic
class StockDataRequest:
    def __init__(self, stock_id: str, start_date: str, end_date: Optional[str] = None):
        self.stock_id = self._validate_stock_id(stock_id)
        self.start_date = self._validate_date(start_date)
        self.end_date = end_date or datetime.now().strftime("%Y-%m-%d")
    
    def _validate_stock_id(self, stock_id: str) -> str:
        if not re.match(r'^\d{4}$', stock_id):
            raise ValueError("Stock ID must be 4 digits")
        return stock_id
    
    def _validate_date(self, date_str: str) -> str:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

# API communication
class TaiwanStockApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def fetch_stock_data(self, request: StockDataRequest) -> List[Dict]:
        parameter = {
            "dataset": "TaiwanStockPrice",
            "data_id": request.stock_id,
            "start_date": request.start_date,
            "end_date": request.end_date,
        }
        return request_get(self.base_url, parameter)
```

#### Violation 2: Main Function Multiple Responsibilities
**File:** `info/TaiwanStockInfo.py` (Lines 37-49)
```python
def main():
    parser = argparse.ArgumentParser(description="Fetch Taiwan Stock Deal Info")
    # ... argument parsing ...
    
    stock_finmind = TaiwanStockInfo()
    stock_deal_info = stock_finmind.get_stock_deal_info(args.stock_id, args.start_date, args.end_date)
    data = pd.DataFrame(stock_deal_info)
    save_to_csv(data, args.output)
```
**Problem:** Main function handles argument parsing, business logic execution, and output formatting.

**Solution:**
```python
class CommandLineInterface:
    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Fetch Taiwan Stock Deal Info")
        parser.add_argument("stock_id", type=str, help="Stock ID (e.g 0050)")
        parser.add_argument("start_date", type=str, help="Start date (e.g 2021-09-13)")
        parser.add_argument("end_date", type=str, nargs="?", default=None, help="End date (YYYY-MM-DD, optional)")
        parser.add_argument("--output", type=str, default="stock_data.csv", help="Output CSV file name")
        return parser.parse_args()

class StockDataService:
    def __init__(self, api_client: TaiwanStockApiClient):
        self.api_client = api_client
    
    def fetch_and_process_data(self, request: StockDataRequest) -> pd.DataFrame:
        raw_data = self.api_client.fetch_stock_data(request)
        return pd.DataFrame(raw_data)

def main():
    cli = CommandLineInterface()
    args = cli.parse_arguments()
    
    request = StockDataRequest(args.stock_id, args.start_date, args.end_date)
    api_client = TaiwanStockApiClient('https://api.finmindtrade.com/api/v4/data')
    service = StockDataService(api_client)
    
    data = service.fetch_and_process_data(request)
    save_to_csv(data, args.output)
```

### 🟡 **Open/Closed Principle (OCP) Violations**

#### Violation: Hard-coded API Dataset
**File:** `info/TaiwanStockInfo.py` (Lines 28-32)
```python
parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": stock_id,
    "start_date": start_date,
    "end_date": end_date,
}
```
**Problem:** Adding support for different datasets requires modifying existing code.

**Solution:** Use strategy pattern for extensibility:
```python
from abc import ABC, abstractmethod

class DatasetStrategy(ABC):
    @abstractmethod
    def build_parameters(self, stock_id: str, start_date: str, end_date: str) -> Dict[str, str]:
        pass

class TaiwanStockPriceStrategy(DatasetStrategy):
    def build_parameters(self, stock_id: str, start_date: str, end_date: str) -> Dict[str, str]:
        return {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": start_date,
            "end_date": end_date,
        }

class TaiwanStockFinancialStrategy(DatasetStrategy):
    def build_parameters(self, stock_id: str, start_date: str, end_date: str) -> Dict[str, str]:
        return {
            "dataset": "TaiwanStockFinancialStatements",
            "data_id": stock_id,
            "start_date": start_date,
            "end_date": end_date,
        }

class TaiwanStockApiClient:
    def __init__(self, base_url: str, strategy: DatasetStrategy):
        self.base_url = base_url
        self.strategy = strategy
    
    def fetch_stock_data(self, request: StockDataRequest) -> List[Dict]:
        parameters = self.strategy.build_parameters(
            request.stock_id, request.start_date, request.end_date
        )
        return request_get(self.base_url, parameters)
```

### 🟡 **Dependency Inversion Principle (DIP) Violations**

#### Violation: Direct Dependency on Concrete Implementation
**File:** `info/TaiwanStockInfo.py` (Lines 12, 34)
```python
from utils.requestUtils import request_get
# ...
data = request_get(self.base_url, parameter)
```
**Problem:** High-level module depends directly on low-level HTTP implementation.

**Solution:** Depend on abstractions:
```python
from abc import ABC, abstractmethod

class HttpClient(ABC):
    @abstractmethod
    def get(self, url: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        pass

class RequestsHttpClient(HttpClient):
    def get(self, url: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        return request_get(url, params)

class TaiwanStockApiClient:
    def __init__(self, base_url: str, http_client: HttpClient, strategy: DatasetStrategy):
        self.base_url = base_url
        self.http_client = http_client
        self.strategy = strategy
    
    def fetch_stock_data(self, request: StockDataRequest) -> List[Dict]:
        parameters = self.strategy.build_parameters(
            request.stock_id, request.start_date, request.end_date
        )
        return self.http_client.get(self.base_url, parameters)
```

### ✅ **SOLID Principles Well Applied**

- **LSP**: No inheritance hierarchies present, so no violations
- **ISP**: Functions are focused and don't force clients to depend on unused methods

## 1. Security Issues

### 🔴 Critical Issues

#### Input Validation Missing
**File:** `info/TaiwanStockInfo.py` (Lines 39-40)
```python
parser.add_argument("stock_id", type=str, help="Stock ID (e.g 0050)")
parser.add_argument("start_date", type=str, help="Start date (e.g 2021-09-13)")
```
**Problem:** No validation for malicious or malformed inputs.
**Risk:** Application crashes, API errors, potential injection attacks.

**Solution:** Implement strict validation (shown in SRP solution above).

#### No Request Timeout
**File:** `utils/requestUtils.py` (Line 6)
```python
r = requests.get(base_url, params=params)
```
**Problem:** Missing timeout could cause indefinite hanging.
**Risk:** DoS vulnerability, resource exhaustion.

**Solution:**
```python
r = requests.get(base_url, params=params, timeout=30)
```

### 🟡 Suggestions

#### Configuration Exposure
**File:** `info/TaiwanStockInfo.py` (Line 16)
```python
self.base_url = 'https://api.finmindtrade.com/api/v4/data'
```
**Issue:** Hard-coded URL should be externalized.

**Solution:**
```python
import os
self.base_url = os.getenv('FINMIND_API_URL', 'https://api.finmindtrade.com/api/v4/data')
```

## 2. Performance & Efficiency

### 🟡 Suggestions

#### Inefficient Path Manipulation
**File:** `info/TaiwanStockInfo.py` (Lines 8-10)
```python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
```
**Problem:** Runtime path manipulation is inefficient.
**Solution:** Use proper package structure with `setup.py`.

#### Memory Usage for Large Datasets
**File:** `info/TaiwanStockInfo.py` (Lines 45-46)
```python
stock_deal_info = stock_finmind.get_stock_deal_info(args.stock_id, args.start_date, args.end_date)
data = pd.DataFrame(stock_deal_info)
```
**Issue:** Loading entire dataset into memory.
**Suggestion:** Implement streaming for large date ranges.

### ✅ Good Practices

- Single API call instead of multiple requests
- Efficient use of pandas for data manipulation

## 3. Code Quality

### 🔴 Critical Issues

#### Bare Exception Handling
**File:** `utils/requestUtils.py` (Lines 12-15)
```python
except Exception as e:
    print(e)
    return None
```
**Problem:** Too broad exception catching masks errors.

**Solution:**
```python
except (ValueError, KeyError, TypeError) as e:
    logger.error(f"JSON parsing error: {e}")
    return None
except requests.exceptions.JSONDecodeError as e:
    logger.error(f"Invalid JSON response: {e}")
    return None
```

#### Inconsistent Error Handling
**File:** `utils/requestUtils.py` (Lines 7-8)
```python
if r.status_code != requests.codes.ok:
    print(f'Error: {r.status_code}')
```
**Problem:** Continues execution after error.

**Solution:**
```python
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    logger.error(f'HTTP error: {e}')
    return None
```

### 🟡 Suggestions

#### Missing Type Hints
**File:** `utils/requestUtils.py` (Line 5)
```python
def request_get(base_url, params):
```
**Solution:**
```python
from typing import Dict, List, Optional, Any
def request_get(base_url: str, params: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
```

#### Inconsistent Naming Conventions
**File:** `utils/csvUtils.py` (Line 5)
```python
def save_to_csv(data: pd.DataFrame, fileName: str):
```
**Issue:** `fileName` should be `file_name` (snake_case).

### ✅ Good Practices

- Clear and descriptive function names
- Good docstring documentation
- Logical separation of concerns

## 4. Architecture & Design

### 🔴 Critical Issues

#### Missing Error Propagation
**File:** `info/TaiwanStockInfo.py` (Lines 34-35)
```python
data = request_get(self.base_url, parameter)
return data
```
**Problem:** No handling if `request_get` returns `None`.

**Solution:**
```python
data = request_get(self.base_url, parameter)
if data is None:
    raise ValueError(f"Failed to fetch data for stock {stock_id}")
return data
```

#### No File Operation Error Handling
**File:** `utils/csvUtils.py` (Lines 7-8)
```python
data.to_csv(fileName, index=False)
print(f"Data saved to {fileName}")
```
**Problem:** No handling for file write failures.

**Solution:**
```python
from pathlib import Path

def save_to_csv(data: pd.DataFrame, file_name: str) -> str:
    try:
        Path(file_name).parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(file_name, index=False)
        logger.info(f"Data saved to {file_name}")
        return os.path.abspath(file_name)
    except PermissionError:
        raise PermissionError(f"Permission denied writing to {file_name}")
    except OSError as e:
        raise OSError(f"File operation failed: {e}")
```

### ✅ Good Practices

- Clean separation between data fetching and saving
- Modular design with utility functions

## 5. Testing & Documentation

### 🔴 Critical Issues

#### Missing Test Coverage
**Problem:** No test files found.
**Risk:** No validation of functionality, difficult refactoring.

**Solution:** Implement comprehensive test suite:
```python
# tests/test_stock_data_service.py
import pytest
from unittest.mock import Mock
from your_app.services import StockDataService, StockDataRequest

class TestStockDataService:
    def setup_method(self):
        self.mock_api_client = Mock()
        self.service = StockDataService(self.mock_api_client)
    
    def test_fetch_and_process_data_success(self):
        # Given
        request = StockDataRequest("0050", "2021-01-01", "2021-01-02")
        self.mock_api_client.fetch_stock_data.return_value = [
            {'date': '2021-01-01', 'close': 100}
        ]
        
        # When
        result = self.service.fetch_and_process_data(request)
        
        # Then
        assert len(result) == 1
        assert result.iloc[0]['close'] == 100
        self.mock_api_client.fetch_stock_data.assert_called_once_with(request)
```

#### Missing Documentation
**Problem:** No README.md or API documentation.

**Solution:** Create comprehensive documentation with usage examples.

### ✅ Good Practices

- Clear docstring in main API method
- Good parameter documentation in argparse

## SOLID Principles Compliance Recommendations

### Immediate Actions for SOLID Compliance

1. **SRP**: Split `TaiwanStockInfo` into separate classes for validation, API communication, and data transformation
2. **OCP**: Implement strategy pattern for different dataset types
3. **DIP**: Create abstractions for HTTP client and inject dependencies
4. **ISP**: Ensure interfaces are focused (current code is acceptable)
5. **LSP**: Design inheritance hierarchies carefully if needed in future

### Architecture Refactor Suggestion

```python
# Dependency injection container
class Container:
    def __init__(self):
        self.http_client = RequestsHttpClient()
        self.strategy = TaiwanStockPriceStrategy()
        self.api_client = TaiwanStockApiClient(
            base_url=os.getenv('FINMIND_API_URL'),
            http_client=self.http_client,
            strategy=self.strategy
        )
        self.service = StockDataService(self.api_client)

def main():
    container = Container()
    cli = CommandLineInterface()
    args = cli.parse_arguments()
    
    request = StockDataRequest(args.stock_id, args.start_date, args.end_date)
    data = container.service.fetch_and_process_data(request)
    save_to_csv(data, args.output)
```

## Priority Action Plan

### 🔴 **Critical (SOLID + Security)**
1. Implement SRP by separating concerns into focused classes
2. Add input validation with proper error handling
3. Implement DIP with dependency injection
4. Add request timeouts and proper exception handling

### 🟡 **High Priority (Architecture + Quality)**
5. Implement OCP with strategy pattern for extensibility
6. Add comprehensive test suite with dependency mocking
7. Create proper logging framework
8. Add configuration management

### **📋 Medium Priority**
9. Improve type hints and documentation
10. Implement proper package structure
11. Add CI/CD pipeline with SOLID principle linting
12. Create API documentation

## Conclusion

The current codebase violates several SOLID principles, particularly SRP and DIP. The main issues are mixed responsibilities within classes and tight coupling to concrete implementations. Implementing the suggested refactoring will significantly improve code maintainability, testability, and extensibility while addressing security and reliability concerns.

The refactored architecture will be more modular, easier to test, and better prepared for future requirements changes.