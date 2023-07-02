#pragma once
#include "Engine/DataTable.h"
#include "FTestData.generated.h"


USTRUCT(BlueprintType)
struct FTestData : public FTableRowBase
{
	GENERATED_BODY()

public:
	FTestData(): Gender(""), Year(""), State(""), Major("") {}

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=College)
	FString Gender;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=College)
	FString Year;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=College)
	FString State;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=College)
	FString Major;
};
