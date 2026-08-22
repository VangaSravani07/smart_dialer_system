from pacing_engine import PacingEngine


engine = PacingEngine(max_calls_per_agent=2)

print("Progressive calls:",
      engine.calculate_progressive_calls(3, 10))

print("Predictive calls:",
      engine.calculate_predictive_calls(3, 10))