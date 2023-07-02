#pragma once

#include "CoreMinimal.h"
#include "IToolModuleInterface.h"
#include "Modules/ModuleManager.h"

class FCustomToolEditorModule : public IToolModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

    virtual void AddModuleListeners() override;

    static inline FCustomToolEditorModule& Get()
    {
        return FModuleManager::LoadModuleChecked<FCustomToolEditorModule>("CustomToolEditor");
    }

    static inline bool IsAvailable()
    {
        return FModuleManager::Get().IsModuleLoaded("CustomToolEditor");
    }

    void AddMenuExtension(const FMenuExtensionDelegate& ExtensionDelegate, FName ExtensionHook,
        const TSharedPtr<FUICommandList>& CommandList = nullptr, EExtensionHook::Position Position = EExtensionHook::Before);

    TSharedRef<FWorkspaceItem> GetMenuRoot() { return MenuRoot; }

protected:
    TSharedPtr<FExtensibilityManager> LevelEditorMenuExtensibilityManager;
    TSharedPtr<FExtender> MenuExtender;

    static TSharedRef<FWorkspaceItem> MenuRoot;

    void MakePulldownMenu(FMenuBarBuilder& MenuBarBuilder);
    void FillPulldownMenu(FMenuBuilder& MenuBuilder);
};
