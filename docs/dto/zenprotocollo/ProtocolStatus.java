package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.config.MessageSourceConfig;
import org.springframework.context.i18n.LocaleContextHolder;

public enum ProtocolStatus {
	DRAFT, CLOSED, CANCELED;

	public String getTranslation(){
		return switch (this) {
			case DRAFT -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-status.draft", null, LocaleContextHolder.getLocale());
			case CLOSED -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-status.closed", null, LocaleContextHolder.getLocale());
			case CANCELED -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-status.canceled", null, LocaleContextHolder.getLocale());
		};
	}
}
