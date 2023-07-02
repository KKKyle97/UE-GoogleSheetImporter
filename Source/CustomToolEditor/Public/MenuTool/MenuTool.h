#pragma once
#include "IToolModuleInterface.h"

class MenuTool : public IToolModuleListenerInterface, public TSharedFromThis<MenuTool>
{
public:
	virtual ~MenuTool() {}

	virtual void OnStartupModule() override;
	virtual void OnShutdownModule() override;

	void MakeMenuEntry(FMenuBuilder& MenuBuilder);

protected:
	TSharedPtr<FUICommandList> CommandList;

	void MapCommands();

	void MenuCommand1();
};