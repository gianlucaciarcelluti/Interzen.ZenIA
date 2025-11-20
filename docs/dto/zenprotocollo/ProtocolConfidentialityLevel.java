package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.config.MessageSourceConfig;
import org.springframework.context.i18n.LocaleContextHolder;

public enum ProtocolConfidentialityLevel {
	PUBLIC, CONFIDENTIAL;

	public String getTranslation(){
		return switch (this) {
			case PUBLIC -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-confidentiality-level.public", null, LocaleContextHolder.getLocale());
			case CONFIDENTIAL -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-confidentiality-level.confidential", null, LocaleContextHolder.getLocale());
		};
	}
}
