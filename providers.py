from enum import Enum


class ProviderResult(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class MockProviderA:

    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def initiate_call(self, phone_number):

        print(
            f"Provider A: Calling {phone_number}"
        )

        if self.should_fail:
            print("Provider A: Call failed")
            return ProviderResult.FAILED

        print("Provider A: Call successful")
        return ProviderResult.SUCCESS


class MockProviderB:

    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def initiate_call(self, phone_number):

        print(
            f"Provider B: Calling {phone_number}"
        )

        if self.should_fail:
            print("Provider B: Call failed")
            return ProviderResult.FAILED

        print("Provider B: Call successful")
        return ProviderResult.SUCCESS