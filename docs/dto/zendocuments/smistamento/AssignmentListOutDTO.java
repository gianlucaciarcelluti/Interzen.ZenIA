package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import java.time.LocalDate;
import java.time.LocalDateTime;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.GroupTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zenprotocollo.ProtocolDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentListOutDTO extends TrackBasicChangesDTO implements HasID<Long>{

    /**
     * The ID of the assignment.
     */
    @Schema(description = "The ID of the assignment.")
    private Long id;
    
    
    /**
     * The ID of the master assignment.
     */
    @Schema(description = "The ID of the master assignment.")
    private Long masterId;

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
    
    
    private Long protocolId;
    
    /*
    @Schema(description = "The protocol number associated with the assignment.")
    private String protocolNumber;
    
   


    @Schema(description = "The correspondent associated with the assignment.")
    private List<String> correspondent;
    */

    /**
     * The date of the assignment.
     */
    @Schema(description = "The date of the assignment.")
    private LocalDateTime assignmentDate;

    /**
     * The office (UOR) associated with the assignment.
     */
    @Schema(description = "The office (UOR) associated with the assignment.")
    private GroupTrackBasicChangesDTO assignmentUOR;

    /**
     * The user associated with the assignment.
     */
    @Schema(description = "The user associated with the assignment.")
    //private Long assignmentUser;
    private UtenteTrackBasicChangesDTO assignmentUser;

    /**
     * The type of the assignment.
     */
    @Schema(description = "The type of the assignment.")
    private AssignmentSlaveType type;

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
	
	@Schema(description = "current action status of a user assignment (slave).")
    private AssignmentSlaveActionStatus actionStatus;
    
    @Schema(description = "current working status of the assignment (master).")
    private AssignmentMasterStatus masterStatus;
    
    @Schema(description = "Processing end date for master.")
    private LocalDateTime masterProcessingDate;
    
    @Schema(description = "Processing end date for slave.")
    private LocalDateTime slaveProcessingDate;


    @Schema(description = "The user who eventually refused the assignment.")
    private UtenteTrackBasicChangesDTO userRejectedAssignment = null;

    @Schema(description = "The reason why the assignment was rejected.")
    private String rejectionReason = null;
    
    
    
}
