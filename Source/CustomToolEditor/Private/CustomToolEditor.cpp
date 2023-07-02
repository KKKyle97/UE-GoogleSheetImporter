#include "CustomToolEditor.h"

#include "LevelEditor.h"
#include "MenuTool/MenuTool.h"

#define LOCTEXT_NAMESPACE "FCustomToolEditorModule"

TSharedRef<FWorkspaceItem> FCustomToolEditorModule::MenuRoot = FWorkspaceItem::NewGroup(FText::FromString("Menu Root"));

void FCustomToolEditorModule::StartupModule()
{
    if (!IsRunningCommandlet())
    {
        FLevelEditorModule& LevelEditorModule = FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor");
        LevelEditorMenuExtensibilityManager = LevelEditorModule.GetMenuExtensibilityManager();
        MenuExtender = MakeShareable(new FExtender);
        MenuExtender->AddMenuBarExtension("Window", EExtensionHook::After, nullptr, FMenuBarExtensionDelegate::CreateRaw(this, &FCustomToolEditorModule::MakePulldownMenu));
        LevelEditorMenuExtensibilityManager->AddExtender(MenuExtender);
    }
    IToolModuleInterface::StartupModule();
}

void FCustomToolEditorModule::ShutdownModule()
{
    IToolModuleInterface::ShutdownModule();
}

void FCustomToolEditorModule::AddModuleListeners()
{
    ModuleListeners.Add(MakeShareable(new MenuTool));
}

void FCustomToolEditorModule::AddMenuExtension(const FMenuExtensionDelegate& ExtensionDelegate, FName ExtensionHook,
    const TSharedPtr<FUICommandList>& CommandList, EExtensionHook::Position Position)
{
    MenuExtender->AddMenuExtension(ExtensionHook, Position, CommandList, ExtensionDelegate);
}

void FCustomToolEditorModule::MakePulldownMenu(FMenuBarBuilder& MenuBarBuilder)
{
    MenuBarBuilder.AddPullDownMenu(
        FText::FromString("Update Datatable"),
        FText::FromString("Update Datatable from json"),
        FNewMenuDelegate::CreateRaw(this, &FCustomToolEditorModule::FillPulldownMenu),
        "Update Datatable",
        FName(TEXT("Update Datatable"))
    );
}

void FCustomToolEditorModule::FillPulldownMenu(FMenuBuilder& MenuBuilder)
{
    MenuBuilder.BeginSection("DatatableSection", FText::FromString("Section 1"));
    MenuBuilder.AddMenuSeparator(FName("Section_1"));
    MenuBuilder.EndSection();
}

#undef LOCTEXT_NAMESPACE
    
IMPLEMENT_MODULE(FCustomToolEditorModule, CustomToolEditor)