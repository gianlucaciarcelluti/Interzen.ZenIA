package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zendocuments.DocumentDTO;
import it.interzen.zencommonlibrary.dto.zenprotocollo.ProtocolDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentDetailsOutDTO  extends TrackBasicChangesDTO{
	
    /**
     * The ID of the assignment.
     */
    @Schema(description = "The ID of the assignment.")
    private Long id;

    /**
     * The title of the assignment.
     */
    @Schema(description = "The title of the assignment.")
    private String title;

    /**
     * The name of the document associated with the assignment.
     */
    @Schema(description = "The name of the document associated with the assignment.")
    private String documentName;
    
    
    /**
     * The date of the assignment.
     */
    @Schema(description = "The date of the assignment.")
    private LocalDateTime assignmentDate;
    
    
    @Schema(description = "current working status of the assignment.")
    private AssignmentMasterStatus assignmentStatus;

    @Schema(description = "The date of the processing of the assignment. (data di lavorazione master)")
    private String masterProcessingDate;
    
    /**
     * The notes associated with the assignment.
     */
    @Schema(description = "The notes associated with the assignment.")
    private String notes; 

    /**
     * The expiration date of the assignment.
     */
    @Schema(description = "The expiration date of the assignment.")
    private String assignmentExpireDate;
    
    
    @Schema(description = "Full data of associated protocol.")
    private ProtocolDTO protocol;
    
    
    @Schema(description = "Full data of the associated document")
    private DocumentDTO document;
    
    @Schema(description = "List of assignees by competence (only one expected)")
    private List<CompetenceAssigneeDTO> competenceAssignees = new ArrayList<>();
    
	@Schema(description = "List of assignees by notification")
	private List<NotificationAssigneeDTO> notificationAssignees = new ArrayList<>();

}
