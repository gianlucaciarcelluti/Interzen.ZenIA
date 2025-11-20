package it.interzen.zencommonlibrary.dto.zenprotocollo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ClassificationOutDTO {
	
    private Long id;
	private String classificationPath;
	private String description;
	private String labelPath;
	private Long schemaNodeId;
	
}
