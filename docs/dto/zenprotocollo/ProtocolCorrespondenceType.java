package it.interzen.zencommonlibrary.dto.zenprotocollo;


import it.interzen.zencommonlibrary.config.MessageSourceConfig;
import org.springframework.context.i18n.LocaleContextHolder;

public enum ProtocolCorrespondenceType {
	CORRIERE, EMAIL, FAX, PEC, POSTA_ORDINARIA, RACCOMANDATA_AR, TELEGRAMMA, A_MANO, PORTALE_WEBSERVICE;


	public String getTranslation(){
		return switch (this) {
			case CORRIERE -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.corriere", null, LocaleContextHolder.getLocale());
			case EMAIL -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.email", null, LocaleContextHolder.getLocale());
			case FAX -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.fax", null, LocaleContextHolder.getLocale());
			case PEC -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.pec", null, LocaleContextHolder.getLocale());
			case POSTA_ORDINARIA -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.posta-ordinaria", null, LocaleContextHolder.getLocale());
			case RACCOMANDATA_AR -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.raccomandata-ar", null, LocaleContextHolder.getLocale());
			case TELEGRAMMA -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.telegramma", null, LocaleContextHolder.getLocale());
			case A_MANO -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.a-mano", null, LocaleContextHolder.getLocale());
			case PORTALE_WEBSERVICE -> MessageSourceConfig.sourceMsg.getMessage("label.protocol-correspondence-type.portale-webservice", null, LocaleContextHolder.getLocale());
		};
	}



}
