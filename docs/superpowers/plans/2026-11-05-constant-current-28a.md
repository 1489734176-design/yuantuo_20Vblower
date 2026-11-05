# 28A Current Regulation Implementation Plan

> **For agentic workers:** Use executing-plans to implement this configuration task in the current session.

**Goal:** Enable average bus current feedback at one 28A target.
**Architecture:** Reuse pwm_set() and its existing calibrated ADC feedback, ramp and duty bounds.
**Tech Stack:** Bare-metal C, MM32SPIN0230, Keil and Arm Compiler 6.
**Spec:** docs/superpowers/specs/2026-11-05-constant-current-28a-design.md

## Global Constraints
Preserve every protection and vendor code; preserve existing generated/IDE changes. Only USER/inc/parameter.h changes production behavior.

## Review Focus
All gears/directions use 28A; calibration remains applied; high current reduces PWM; lower current recovers within trigger/duty bounds; existing protection handling is untouched.

## Task 1: Enable existing regulator
- [x] Add CONSTANT_BUS_CURRENT=28.0f, enable LIMIT_AVG_CURRENT_EN and alias its five current selections to the shared target.
- [x] Clean rebuild in an isolated output directory with AC6, reviewing every warning; also verify compatibility with the project's existing AC5 setting.
- [x] Inspect pwm_set machine code for the 249-count calibrated-current comparison and retained up/down PWM branches.
- [x] Review source diff and provide firmware with honest hardware-validation limits. Leave source edits reviewable without making an unsolicited commit.
