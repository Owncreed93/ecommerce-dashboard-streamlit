"""Cloud Data Provider infrastructure adapter for local testing."""

from domain.data_provider_interface import DataProvider


class LocalFileDataProvider(DataProvider):
    """Infrastructure adapter for local file-based data sourcing."""

    def __init__(self, file_path: str) -> None:
        """Initializes the provider with a local file path.

        Args:
            file_path: The path to the local CSV file.
        """
        self.file_path = file_path

    def ensure_data_is_available(self) -> str:
        """Ensures the dataset is locally available.

        Returns:
            The local file path.
        """
        return self.file_path
