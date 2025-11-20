package it.interzen.zencommonlibrary.dto.zenmailroom;

import java.util.Date;
import java.util.List;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
public class SendingLogDTO extends TableLookupEntityDTOGLongPK<SendingLogDTO> implements LookupEntityGReturnLongPK<SendingLogDTO> {  
    String ipaddress;
	String smtphost;
	int smtpport;
	String mailsender;
	String mailrecipient;
	String mailcc;
    String mailsubject;
    String headers;
    String error;
    Long mailboxid; // Non metto fk perché il log deve sopravvivere ad eventuali cancellazioni
    String mailmessageid;
    Long companyid;
    Long aooid;
    Date maildatetime = new Date(); // Da verificare bene il fuso orario
    Long templateid;
    UtenteTrackBasicChangesDTO userid;
    
    @Enumerated(EnumType.STRING)
    ObjectSourceTypeEnum objectsourcetype = ObjectSourceTypeEnum.DOCUMENT;
    
	Long objectsourceid;
	Long sentdocumentid;
	String sentdocumenttoken;
	Integer[] attachmentdocumentids;

	@Enumerated(EnumType.STRING)
	SendingLogStatusEnum status = SendingLogStatusEnum.NONE;

	String undeliveredRecipients;
	
	List<ReceivingLogDTO> receivinglogs;
    
	@Override
	public String getDescription() {
		return null;
	}
	
	@Override
	public String getCode() {
		return null;
	}
}
