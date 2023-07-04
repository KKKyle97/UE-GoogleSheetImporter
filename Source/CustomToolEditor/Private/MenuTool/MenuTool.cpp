#include "MenuTool/MenuTool.h"

#include "CustomToolEditor.h"
#include "EditorAssetLibrary.h"
#include "EditorStyleSet.h"
#include "EditorUtilitySubsystem.h"
#include "EditorUtilityWidgetBlueprint.h"

#define LOCTEXT_NAMESPACE "MenuTool"

class MenuToolCommands : public TCommands<MenuToolCommands>
{
public:
	MenuToolCommands()
		: TCommands<MenuToolCommands>(
			TEXT("MenuTool"),
			FText::FromString("Example Menu Tool"),
			NAME_None,
			FAppStyle::GetAppStyleSetName()
		)
	{}

	virtual void RegisterCommands() override
	{
		UI_COMMAND(MenuCommand1, "Update Datatable", "Click to open datatable updater", EUserInterfaceActionType::Button, FInputGesture());
	}

public:
	TSharedPtr<FUICommandInfo> MenuCommand1;
};

void MenuTool::OnStartupModule()
{
	CommandList = MakeShareable(new FUICommandList);
	MenuToolCommands::Register();
	MapCommands();
	FCustomToolEditorModule::Get().AddMenuExtension(
		FMenuExtensionDelegate::CreateRaw(this, &MenuTool::MakeMenuEntry),
		FName("Section_1"),
		CommandList
	);
}

void MenuTool::OnShutdownModule()
{
	MenuToolCommands::Unregister();
}

void MenuTool::MakeMenuEntry(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.AddMenuEntry(MenuToolCommands::Get().MenuCommand1);
}

void MenuTool::MapCommands()
{
	const auto& Commands = MenuToolCommands::Get();

	CommandList->MapAction(
		Commands.MenuCommand1,
		FExecuteAction::CreateSP(this, &MenuTool::MenuCommand1),
		FCanExecuteAction()
	);
}

void MenuTool::MenuCommand1()
{
	const FString PathToDatabaseSelector = "/Game/EditorUtility/DatabaseSelector";

	UE_LOG(LogTemp, Warning, TEXT("Database Selector Path: %s"), *PathToDatabaseSelector);

	UObject* WidgetObject = UEditorAssetLibrary::LoadAsset(PathToDatabaseSelector);

	if (UEditorUtilityWidgetBlueprint* DatabaseSelector = Cast<UEditorUtilityWidgetBlueprint>(WidgetObject))
	{
		if (UEditorUtilitySubsystem* EditorUtilitySubsystem = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>())
		{
			EditorUtilitySubsystem->SpawnAndRegisterTab(DatabaseSelector);
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("Unable to open database selector"));
		}
	}
}

#undef LOCTEXT_NAMESPACE