package it.interzen.zencommonlibrary.dto.zendocuments;


import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import io.swagger.v3.oas.annotations.media.Schema;

import it.interzen.zencommonlibrary.basedb.Searchable;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(name="Document", description="Documento con le sue proprietà")
@JsonPropertyOrder({
		"id",
		"fileName",
		"description",
		"source",
		"folderId",
		"model",
		"isAttachment",
		"attachmentType",
		"status",
		"mimeType",
		"inheritPermission",
		"metadata",
		"barCode",
		"statusWorkflow",
		"statusAssignment",
		"statusLegalArchive",
		"statusRegistration"
})
public class DocumentDTO extends DocumentBaseDTO implements Searchable {
	private Long size;
	
	private Long totalSizeAllVersion;

	private Integer version = 1;

	private Integer subVersion = 0;
	
	private Integer versionKarchive;

	@Enumerated(EnumType.STRING)
	private DocumentStatusWorkFlow statusWorkflow;

	@Enumerated(EnumType.STRING)
	private DocumentStatusAssignment statusAssignment;

	@Enumerated(EnumType.STRING)
	private DocumentStatusRegistration statusRegistration;

	private LocalDateTime archiveCurrentDate;   //Data in cui il documento è stato messo in stato archiviato

	private LocalDateTime archiveDepositDate;   //Data in cui il documento è stato fascicolato

	private LocalDateTime archiveHistoricalDate;   //Data in cui il documento è stato messo storicizzato

	private UtenteTrackBasicChangesDTO archiveCurrentBy;     // Utente che ha impostato lo stato fascicolato
	private UtenteTrackBasicChangesDTO archiveDepositBy;     // Data in cui il documento è stato messo storicizzato
	private UtenteTrackBasicChangesDTO archiveHistoricalBy;  // utente che ha storicizzato

	private LocalDateTime dateDelete;   //Data in cui il documento è stato smaltito

	private String hash;
	
	private String hashAlgorithm;

	private Long registrationId;

	// Documenti riservati (protocollo)
	private Boolean isReserved;

	// Elenco della breadcrumb
	List<BreadcrumbItem> breadcrumb;

	private DocumentTypeEnum type = DocumentTypeEnum.DOCUMENT;

	private Long classificationSchemaCompanyId;
	private Long classificationSchemaAaooId;
	private Long classificationSchemaId;

	private Boolean electronicallySealed;
	private Boolean timestampMark;
	private Boolean conformityImageCopiesOnComputerMedia;
	private Boolean isDigitalSigned;

	private String docToken;

	private String metadataStringSearch;


	@Override
	public String createSearchString() {
		String folderName = "";
		if (folderId != null) {
			folderName = folderId.getName();
		}
		String modelName = "";
		if (model != null) {
			modelName = model.getName();
		}

		String statusLegalArchiveString = "";
		if (statusLegalArchive != null) {
			statusLegalArchiveString = statusLegalArchive.toString();
		}

		String statusWorkflowString = "";
		if (statusWorkflow != null) {
			statusWorkflowString = statusWorkflow.toString();
		}

		String statusRegistrationString = "";
		if (statusRegistration != null) {
			statusRegistrationString = statusRegistration.toString();
		}

		String externalReferenceString = "";
		if (externalReference != null) {
			externalReferenceString = externalReference;
		}

		String processKeyString = "";
		if (processKey != null) {
			processKeyString = processKey;
		}

        String processDocumentTypeString = "";
        if (getProcessDocumentType() != null) {
            processDocumentTypeString = getProcessDocumentType() ;
        }

		String barCodeString = "";
		if (barCode != null) {
			barCodeString = barCode;
		}

		String metadataString = metadataStringSearch;

		return
				description + " " + fileName + " " + note
						+ " " + folderName + " " + modelName
						+ " " + barCodeString + " " + status
						+ " " + statusLegalArchiveString + " " + statusWorkflowString
						+ " " + statusRegistrationString
						+ " " + externalReferenceString + " " + processKeyString + " " + processDocumentTypeString
						+ " " + metadataString
				;
	}
}
