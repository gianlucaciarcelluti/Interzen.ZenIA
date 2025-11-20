package it.interzen.zencommonlibrary.dto.zenmailroom;

import java.time.LocalDateTime;
import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.CompanyTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.ProtAOOTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = false)
@AllArgsConstructor
@NoArgsConstructor
public class EmailParameterDTO extends TrackBasicChangesDTO implements HasID<Long>, LookupEntityGReturnLongPK<EmailParameterDTO> {
	private Long id;
	private String description; 
	private String emailaddress; 
	private String username;
	private String password;
	
	@Schema(description = "Email Type - 1=Email - 3=PEC (ZenShare compatibility)")
    private int emailtype = 1;
    
    @Schema(description = "Authentication - NONE - BASIC - MICROSOFT_OAUTH")
    @Enumerated(EnumType.STRING)
    private EmailParameterAuthEnum auth = EmailParameterAuthEnum.BASIC;
    
	private String smtphost;
    private int smtpport; 
    
    @Schema(description = "Parametri SMTP separati da virgola")
    private String smtpparameters;
    private String imaphost;
    private int imapport;
    
    @Schema(description = "Protocollo IMAP da utilizzare [imap|imaps]")
    private String imapprot = "imaps";
    private String imapparameters;
    
    @Schema(description = "Cartelle IMAP da leggere separate da virgola")
    private String imapfolders = "INBOX";
    private int defaultsmtp = 0;
    private int outbound = 1;
    private int inbound = 1;
    private Long inboundfolderid;
    private String modelcode;
    private String sender;
    private LookupElementDTOLong<OauthEmailParameterDTO> oauthemailparameter;
	private LookupElementDTOLong<EmailSignatureDTO> emailsignature;

	private CompanyTrackBasicChangesDTO companyid;
	private ProtAOOTrackBasicChangesDTO aooid;
	
	private String errorDescription;
	private LocalDateTime errorData;
    private int errorCount = 0;
    private Boolean sendProtocolClosedNotifications = false;
	
	@Override
	public String getCode() {
		return null;
	}
	
	public void setCode(String code) {
		// necessario altrimenti non si riesce a fare il deserialize 
	}
}
