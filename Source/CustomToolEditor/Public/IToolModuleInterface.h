#pragma once

class IToolModuleListenerInterface
{
public:
	virtual ~IToolModuleListenerInterface() = default;
	virtual void OnStartupModule() {};
	virtual void OnShutdownModule() {};
};

class IToolModuleInterface : public IModuleInterface
{
public:
	void StartupModule() override
	{
		if (!IsRunningCommandlet())
		{
			AddModuleListeners();
			for (int32 i = 0; i < ModuleListeners.Num(); i++)
			{
				ModuleListeners[i]->OnStartupModule();
			}
		}
	}

	void ShutdownModule() override
	{
		for (int32 i = 0; ModuleListeners.Num(); i++)
		{
			if (ModuleListeners[i].ToSharedPtr().IsValid())
			{
				ModuleListeners[i]->OnShutdownModule();
			}
		}
	}

	virtual void AddModuleListeners() {};

protected:
	TArray<TSharedRef<IToolModuleListenerInterface>> ModuleListeners;
};
