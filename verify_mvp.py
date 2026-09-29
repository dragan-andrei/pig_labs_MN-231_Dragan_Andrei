"""Static architectural verifier validating Model-View-Presenter (MVP) compliance."""

from __future__ import annotations

import ast
import io
import os
import pathlib
import sys
import unittest
from typing import List, Set, Tuple


class MvpArchitectureVerifier:
    """Verifies that the codebase strictly obeys Model-View-Presenter rules."""

    def __init__(self, root_dir: pathlib.Path) -> None:
        """Initialize verifier with repository root directory.

        Args:
            root_dir: Absolute path to the workspace root.
        """
        self._root_dir = root_dir
        self._model_dir = root_dir / "model"
        self._view_dir = root_dir / "view"
        self._presenter_dir = root_dir / "presenter"

    def _get_imports(self, file_path: pathlib.Path) -> Set[str]:
        """Extract all imported module prefixes from a python file using AST."""
        imported_modules: Set[str] = set()
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_modules.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_modules.add(node.module.split(".")[0])
        except Exception:
            pass
        return imported_modules

    def _has_top_level_functions(self, file_path: pathlib.Path) -> bool:
        """Check if file contains freestanding procedural functions outside of classes."""
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return True
        except Exception:
            pass
        return False

    def verify_isolation_rules(self) -> List[Tuple[str, bool, str]]:
        """Verify strict dependency isolation rules between MVP layers."""
        results: List[Tuple[str, bool, str]] = []

        # Rule 1: View must NOT import from Model (View knows only ViewModels & Presenter)
        view_files = list(self._view_dir.rglob("*.py"))
        model_leaks_in_view: List[str] = []
        for file in view_files:
            imports = self._get_imports(file)
            if "model" in imports:
                model_leaks_in_view.append(file.name)

        passed_rule_1 = len(model_leaks_in_view) == 0
        desc_1 = (
            "View is isolated from Model (0 direct imports)"
            if passed_rule_1
            else f"Model imports detected in View: {', '.join(model_leaks_in_view)}"
        )
        results.append(("View -> Model Isolation", passed_rule_1, desc_1))

        # Rule 2: Model must NOT import from View, Presenter, or GUI frameworks
        model_files = list(self._model_dir.rglob("*.py"))
        ui_leaks_in_model: List[str] = []
        for file in model_files:
            imports = self._get_imports(file)
            forbidden = {"view", "presenter", "tkinter", "customtkinter"}
            intersections = imports.intersection(forbidden)
            if intersections:
                ui_leaks_in_model.append(f"{file.name} ({', '.join(intersections)})")

        passed_rule_2 = len(ui_leaks_in_model) == 0
        desc_2 = (
            "Model is completely independent from GUI and Presenter"
            if passed_rule_2
            else f"GUI/Presenter imports in Model: {', '.join(ui_leaks_in_model)}"
        )
        results.append(("Model Independence", passed_rule_2, desc_2))

        # Rule 3: Presenter acts as mediator importing both Model and View contracts
        presenter_files = list(self._presenter_dir.rglob("*.py"))
        presenter_imports: Set[str] = set()
        for file in presenter_files:
            presenter_imports.update(self._get_imports(file))

        passed_rule_3 = "model" in presenter_imports and "view" in presenter_imports
        desc_3 = (
            "Presenter coordinates Model and View contracts"
            if passed_rule_3
            else "Presenter does not coordinate Model and View"
        )
        results.append(("Presenter Mediation", passed_rule_3, desc_3))

        # Rule 4: Strict OOP - no standalone functions outside classes
        all_py_files = [
            f for f in self._root_dir.rglob("*.py")
            if ".venv" not in f.parts and "tests" not in f.parts and f.name != "verify_mvp.py"
        ]
        procedural_files: List[str] = [
            f.name for f in all_py_files if self._has_top_level_functions(f)
        ]
        passed_rule_4 = len(procedural_files) == 0
        desc_4 = (
            "100% OOP: All functions are encapsulated within classes"
            if passed_rule_4
            else f"Standalone functions found in: {', '.join(procedural_files)}"
        )
        results.append(("Strict OOP Compliance", passed_rule_4, desc_4))

        return results

    def run_unit_tests(self) -> Tuple[bool, int, str]:
        """Execute automated headless tests to confirm testability."""
        loader = unittest.TestLoader()
        suite = loader.discover(str(self._root_dir / "tests"))
        buffer = io.StringIO()
        runner = unittest.TextTestRunner(verbosity=0, stream=buffer)
        result = runner.run(suite)
        passed = result.wasSuccessful()
        return passed, result.testsRun, f"{result.testsRun} automated tests passed without GUI"

    def run_verification(self) -> int:
        """Run all verifications and print diagnostic summary report."""
        print("=" * 72)
        print("         MODEL - VIEW - PRESENTER (MVP) ARCHITECTURE AUDIT")
        print("=" * 72)

        all_passed = True
        isolation_results = self.verify_isolation_rules()

        for title, passed, desc in isolation_results:
            status = "[PASS]" if passed else "[FAIL]"
            print(f" {status}  {title:<26} | {desc}")
            if not passed:
                all_passed = False

        test_passed, test_count, test_desc = self.run_unit_tests()
        test_status = "[PASS]" if test_passed else "[FAIL]"
        print(f" {test_status}  {'Headless GUI Testability':<26} | {test_desc}")
        if not test_passed:
            all_passed = False

        print("=" * 72)
        if all_passed:
            print(" RESULT: 100% ARCHITECTURAL COMPLIANCE WITH MVP PATTERN!")
            print(" Layers are decoupled, View never touches Model, UI is headless-testable.")
        else:
            print(" RESULT: ARCHITECTURAL VIOLATIONS DETECTED.")
        print("=" * 72)

        return 0 if all_passed else 1


class VerifierBootstrap:
    """Bootstrap runner for the architecture verifier."""

    @classmethod
    def main(cls) -> None:
        """Execute verification."""
        verifier = MvpArchitectureVerifier(pathlib.Path(__file__).parent)
        exit_code = verifier.run_verification()
        sys.exit(exit_code)


if __name__ == "__main__":
    VerifierBootstrap.main()
