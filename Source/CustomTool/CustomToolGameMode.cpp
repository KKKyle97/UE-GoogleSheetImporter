// Copyright Epic Games, Inc. All Rights Reserved.

#include "CustomToolGameMode.h"
#include "CustomToolCharacter.h"
#include "UObject/ConstructorHelpers.h"

ACustomToolGameMode::ACustomToolGameMode()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnBPClass(TEXT("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"));
	if (PlayerPawnBPClass.Class != NULL)
	{
		DefaultPawnClass = PlayerPawnBPClass.Class;
	}
}
