import app.i18n as i18n


def test_t_returns_polish_translation():
    """Test that t returns a Polish translation for a known key."""
    assert i18n.t("pl", "task_list_header") == "Lista zadań"


def test_t_returns_english_translation():
    """Test that t returns an English translation for a known key."""
    assert i18n.t("en", "task_list_header") == "Task list"


def test_t_falls_back_to_default_lang_on_unknown_lang():
    """Test that unknown language falls back to DEFAULT_LANG translations."""
    assert i18n.t("xx", "title") == i18n.t(i18n.DEFAULT_LANG, "title")


def test_t_returns_key_when_missing_translation_key():
    """Test that missing translation key falls back to returning the key itself."""
    assert i18n.t("pl", "this_key_does_not_exist") == "this_key_does_not_exist"
    assert i18n.t("en", "this_key_does_not_exist") == "this_key_does_not_exist"


def test_t_handles_none_lang():
    """Test that None language is handled and falls back to DEFAULT_LANG."""
    assert i18n.t(None, "title") == i18n.t(i18n.DEFAULT_LANG, "title")