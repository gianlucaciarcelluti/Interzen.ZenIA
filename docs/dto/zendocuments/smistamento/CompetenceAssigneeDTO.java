package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.dto.GroupTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CompetenceAssigneeDTO {
	
	private Long id;
	private GroupTrackBasicChangesDTO uorCompetenceId;
	private UtenteTrackBasicChangesDTO userCompetenceAssignedId;
	private AssignmentActionsAllowed operations = new AssignmentActionsAllowed();
	
    
    @Schema(description = "current action status of a user assignment.")
    private AssignmentSlaveActionStatus actionStatus;

	
}
