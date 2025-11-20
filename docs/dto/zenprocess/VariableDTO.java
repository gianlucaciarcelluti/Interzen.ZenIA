package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class VariableDTO {
	String taskId;
    String variableId;
    Object variableValue;
}
