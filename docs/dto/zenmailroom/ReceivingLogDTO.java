package it.interzen.zencommonlibrary.dto.zenmailroom;

import java.util.Date;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = false)
@AllArgsConstructor
@NoArgsConstructor
public class ReceivingLogDTO extends TableLookupEntityDTOGLongPK<ReceivingLogDTO> implements HasID<Long>, LookupEntityGReturnLongPK<ReceivingLogDTO> {
	private Long id;
	private String imaphost;
	private int imapport = 0;
	private String mailfolder = "INBOX";
	private String username;
	private String mailsender;
	private String mailrecipient;
	private String mailcc;
    private String mailsubject;
    private String error;
    private LookupElementDTOLong<EmailParameterDTO> mailboxid;
    private String mailmessageid;
    private String mailxreceived;
    private String mailxrefmessageid;
    private Date mailxreceiveddate;
    private String mailxreceivedrcpt;
    private String mailxreceivederror;
    private Long mailxreceivedsendinglogid;
	
    private Long companyid;
    private Long aooid;
    private Date maildatetime;
    private String receivingpath;
    
    private UtenteTrackBasicChangesDTO userid;
    
    private Long documentid;
    private String documenttoken;

	@Override
	public String getCode() {
		return null;
	}

	@Override
	public String getDescription() {
		return null;
	}
}
