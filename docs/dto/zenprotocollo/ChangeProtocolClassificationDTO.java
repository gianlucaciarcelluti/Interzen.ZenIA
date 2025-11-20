package it.interzen.zencommonlibrary.dto.zenprotocollo;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChangeProtocolClassificationDTO {
	
	@NotNull
	private Long protocolId;
	
	@NotNull
	private Long ClassificationSchemaFolderId;
	
	private Long dossierFolderId = null;
}
