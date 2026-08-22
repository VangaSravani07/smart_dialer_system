from providers import MockProviderA, MockProviderB


print("Testing successful call:")

provider_a = MockProviderA(
    should_fail=False
)

result = provider_a.initiate_call(
    "9876543210"
)

print("Result:", result.value)


print("\nTesting failed call:")

provider_b = MockProviderB(
    should_fail=True
)

result = provider_b.initiate_call(
    "9876543211"
)

print("Result:", result.value)