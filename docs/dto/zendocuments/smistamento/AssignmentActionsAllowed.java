package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class AssignmentActionsAllowed {
	
	
	private boolean accept = false;
	private boolean assignToMe = false;
	private boolean assignToOther = false;
	private boolean archive = false;
	private boolean worked = false;
	private boolean reject = false;
	private boolean viewed = false;
	
}
