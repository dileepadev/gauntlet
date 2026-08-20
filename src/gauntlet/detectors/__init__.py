"""Shared detection primitives.

A detector reads a trace and answers exactly one question: did the harmful
effect occur? It never reads the model's prose — a model can refuse eloquently
in text while calling the tool anyway, so text is not evidence.

The primitives that cases compose from land in milestone 0.4.
"""
