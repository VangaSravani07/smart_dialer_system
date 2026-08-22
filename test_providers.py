from providers import MockProviderA, MockProviderB


provider_a = MockProviderA()
provider_b = MockProviderB()

result_a = provider_a.initiate_call("9876543210")
result_b = provider_b.initiate_call("9876543211")

print("Provider A result:", result_a.value)
print("Provider B result:", result_b.value)