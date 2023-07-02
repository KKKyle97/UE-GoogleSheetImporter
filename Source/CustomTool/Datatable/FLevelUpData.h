#pragma once
#include "Engine/DataTable.h"
#include "FLevelUpData.generated.h"

USTRUCT(BlueprintType)
struct FLevelUpData : public FTableRowBase
{
	GENERATED_BODY()

public:
	FLevelUpData(): XPtoLvl(0), AdditionalHP(0){}

	/** The 'Name' column is the same as the XP Level */

	/** XP to get to the given level from the previous level */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=LevelUp)
	int32 XPtoLvl;

	/** Extra HitPoints gained at this level */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category=LevelUp)
	int32 AdditionalHP;

};
