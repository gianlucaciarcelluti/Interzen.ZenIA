package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssignmentMakeActionDTO {

	@NotNull
	private Long assignmentId;
	
	@NotNull
	private AssignmentActionsEnum action;
	
	private String reason = null;
	
	private Long assignmentUserId = null;
	
}
