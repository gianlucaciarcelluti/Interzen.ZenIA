package it.interzen.zencommonlibrary.dto.zenadmin;

public enum RequireActions {
	CONFIGURE_TOTP("CONFIGURE_TOTP"),
	UPDATE_PASSWORD("UPDATE_PASSWORD"),
	UPDATE_PROFILE("UPDATE_PROFILE"),
	VERIFY_EMAIL("VERIFY_EMAIL"),
	webauthn_register("webauthn-register"),
	webauthn_register_passwordless("webauthn-register-passwordless"),
	update_user_locale("update_user_locale");
	
	
	String data;
	RequireActions(String s) {
		data = s;
	}
	
	public String toString() {
		return data;
	}
};
