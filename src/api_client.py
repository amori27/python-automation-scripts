"""API Client Module.

This module provides utilities for API integration
including REST API calls, authentication, and rate limiting.
"""

import requests
import time
from typing import Any


class APIClient:
    """Handles API requests with rate limiting."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        rate_limit: int = 10
    ):
        """Initialize the APIClient.

        Args:
            base_url: Base URL for API.
            api_key: Optional API key.
            rate_limit: Max requests per second.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.last_request = 0

        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _rate_limit_wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_request
        min_interval = 1.0 / self.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self.last_request = time.time()

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make GET request.

        Args:
            endpoint: API endpoint.
            params: Query parameters.

        Returns:
            Response data.
        """
        self._rate_limit_wait()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=30)

        if response.status_code == 200:
            return response.json()
        return {"error": f"Status {response.status_code}"}

    def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make POST request.

        Args:
            endpoint: API endpoint.
            data: Request body.

        Returns:
            Response data.
        """
        self._rate_limit_wait()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data, timeout=30)

        if response.status_code in [200, 201]:
            return response.json()
        return {"error": f"Status {response.status_code}"}

    def put(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make PUT request.

        Args:
            endpoint: API endpoint.
            data: Request body.

        Returns:
            Response data.
        """
        self._rate_limit_wait()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=data, timeout=30)

        if response.status_code == 200:
            return response.json()
        return {"error": f"Status {response.status_code}"}

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make DELETE request.

        Args:
            endpoint: API endpoint.

        Returns:
            Response data.
        """
        self._rate_limit_wait()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url, timeout=30)

        if response.status_code in [200, 204]:
            return {"success": True}
        return {"error": f"Status {response.status_code}"}

    def close(self) -> None:
        """Close the session."""
        self.session.close()


def paginate_api(
    client: APIClient,
    endpoint: str,
    page_param: str = "page",
    limit_param: str = "limit"
) -> list[dict[str, Any]]:
    """Paginate through API results.

    Args:
        client: APIClient instance.
        endpoint: API endpoint.
        page_param: Page parameter name.
        limit_param: Limit parameter name.

    Returns:
        Combined results from all pages.
    """
    all_results = []
    page = 1

    while True:
        response = client.get(endpoint, params={page_param: page, limit_param: 100})

        if "error" in response:
            break

        data = response.get("data", [])
        if not data:
            break

        all_results.extend(data)
        page += 1

        if response.get("total_pages", 0) < page:
            break

    return all_results
