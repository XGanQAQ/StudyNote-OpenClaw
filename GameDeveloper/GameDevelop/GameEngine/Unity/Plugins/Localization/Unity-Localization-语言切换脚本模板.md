## 模板 语言切换脚本
使用AsyncOperationHandle 保证语言资源已经加载完毕，提前加载语言数据
```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Localization;
using UnityEngine.Localization.Settings;
using UnityEngine.ResourceManagement.AsyncOperations;

public class LanguageManager : MonoBehaviour
{
    AsyncOperationHandle m_InitializeOperation;
    private Locale _chineseLocale;
    private Locale _englishLocale;

    void Start()
    {
        // SelectedLocaleAsync will ensure that the locales have been initialized and a locale has been selected.
        m_InitializeOperation = LocalizationSettings.SelectedLocaleAsync;
        if (m_InitializeOperation.IsDone)
        {
            InitializeCompleted(m_InitializeOperation);
        }
        else
        {
            m_InitializeOperation.Completed += InitializeCompleted;
        }
    }

    void InitializeCompleted(AsyncOperationHandle obj)
    {
        var locales = LocalizationSettings.AvailableLocales.Locales;
        for (int i = 0; i < locales.Count; ++i)
        {
            var locale = locales[i];
            if (locale.LocaleName == "Chinese (Simplified) (zh)")
            {
                _chineseLocale = locale;
            }
            else if (locale.LocaleName == "English (en)")
            {
                _englishLocale = locale;
            }
        }
    }

    public void SwitchChinese()
    {
        LocalizationSettings.Instance.SetSelectedLocale(_chineseLocale);
    }

    public void SwitchEnglish()
    {
        LocalizationSettings.Instance.SetSelectedLocale(_englishLocale);
    }
}
```

暴力切换版本
```cs
using UnityEngine;
using UnityEngine.Localization.Settings;

public class LanguageManager : MonoBehaviour
{
    public void SwitchChinese()
    {
        LocalizationSettings.SelectedLocale = LocalizationSettings.AvailableLocales.Locales[0];
    }

    public void SwitchEnglish()
    {
        LocalizationSettings.SelectedLocale = LocalizationSettings.AvailableLocales.Locales[1];
    }
}
```