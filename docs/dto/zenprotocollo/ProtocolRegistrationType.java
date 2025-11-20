package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.config.MessageSourceConfig;
import org.springframework.context.i18n.LocaleContextHolder;

public enum ProtocolRegistrationType {

	INBOX, OUTBOX, INTERNAL;


	public String getTranslation(){
        return switch (this) {
            case INBOX -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-registration-type.inbox", null, LocaleContextHolder.getLocale());
            case OUTBOX -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-registration-type.outbox", null, LocaleContextHolder.getLocale());
            case INTERNAL -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-registration-type.internal", null, LocaleContextHolder.getLocale());
        };
	}

}
