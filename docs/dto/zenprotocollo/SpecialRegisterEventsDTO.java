package it.interzen.zencommonlibrary.dto.zenprotocollo;

import java.time.LocalDateTime;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zendocuments.DocumentFlowTypeEnum;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SpecialRegisterEventsDTO extends TrackBasicChangesDTO implements HasID<Long> {
    private Long id;
	private Long specialRegisterTypeId;
	
	@NotNull
	private Long companyid;
	
	@NotNull
	private Long aooid;
	
	@NotNull
	private String progressiveNumber;
    
	@NotNull
	private Long registeredBy;
	
	@NotNull
	private LocalDateTime registrationTimestamp;
	
	@NotNull
	private Integer year = LocalDateTime.now().getYear();
	
	private String object;
	private ClassificationOutDTO classificationId;
	
	@NotNull
    private Boolean isReserved = false;
	private DocumentFlowTypeEnum flowType;
	
	@NotNull
	private Long documentId;
	private Long folderId;
	private String registryCode;
	private String documentHash;
	private String documentHashAlgorithm;
	private Long signatureDocumentId;
	
	@NotNull
    private RegisterStatus registerStatus;
	
	@NotNull
	private RegisterActionEnum registerAction;
	
	// Optional info
	
	private Long[] documentAttachmentIds;
	private String[] documentAttachmentHashes;
	private String[] documentAttachmentHashAlgorithms;
	private String registryProducerCode;
	private LocalDateTime registryFirstDate;
	private String[] correspondents;
	private String[] responsibilitiesAndSkills;
}
