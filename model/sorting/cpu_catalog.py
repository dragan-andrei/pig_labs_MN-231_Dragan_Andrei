"""Reference CPU benchmark database providing performance scores."""

from __future__ import annotations

from typing import ClassVar, Dict


class CpuPowerCatalog:
    """Benchmark reference scores used to evaluate and compare CPU computing power."""

    _SCORES: ClassVar[Dict[str, int]] = {
        "Intel Core i3": 9000,
        "Intel Core i5": 15000,
        "Intel Core i7": 22000,
        "Intel Core i9": 30000,
        "AMD Ryzen 3": 9500,
        "AMD Ryzen 5": 18000,
        "AMD Ryzen 7": 24000,
        "AMD Ryzen 9": 34000,
        "Intel Core i5-13400": 25000,
        "AMD Ryzen 5 5600X": 22000,
        "Apple M1": 14500,
        "Apple M2": 16000,
        "Apple M3": 20500,
        "Intel Core i5-1240P": 17500,
        "Intel Core i7-12700H": 27500,
        "AMD Ryzen 7 6800U": 21500,
        "Intel Core Ultra 7": 29000,
        "AMD Ryzen 9 7940HS": 31500,
        "Apple M2 Pro": 24500,
        "Apple M3 Max": 48000,
        "AMD EPYC 7763": 64000,
        "AMD EPYC 9654": 96000,
        "Intel Xeon Silver 4314": 22000,
        "Intel Xeon Gold 6330": 40000,
        "Intel Xeon Platinum 8380": 54000,
        "AMD EPYC 7543": 56000,
        "Intel Xeon E-2388G": 18000,
        "AMD EPYC 9354": 60000,
        "Intel Xeon Gold 5418Y": 36000,
        "AMD EPYC 7713": 52000,
    }

    @classmethod
    def score_for(cls, cpu_name: object) -> int:
        """Return benchmark score for a given CPU model name.

        Args:
            cpu_name: The processor identifier string or object.

        Returns:
            Integer benchmark score (default 0 if unknown).
        """
        return cls._SCORES.get(str(cpu_name).strip(), 0)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(total_models={len(self._SCORES)})"
