package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.dto.GroupTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class NotificationAssigneeDTO {

	private Long id;
	//private Long assigneeId;
	private UtenteTrackBasicChangesDTO userAssigneeId;
	private GroupTrackBasicChangesDTO uorAssigneeId;
	private NotificationAssigneeType assigneeType;
	private AssignmentActionsAllowed operations = new AssignmentActionsAllowed();
    
    @Schema(description = "current action status of a user assignment.")
    private AssignmentSlaveActionStatus actionStatus;
	
	
}
