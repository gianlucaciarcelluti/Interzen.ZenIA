package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MessageCorrelationRequestDTO {
    private String messageName;
    private String processInstanceId;
    private Map<String, Object> variables;
}
