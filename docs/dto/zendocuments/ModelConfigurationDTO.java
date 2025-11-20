package it.interzen.zencommonlibrary.dto.zendocuments;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class ModelConfigurationDTO implements HasID<Long> {
	private Long id;

	@NotNull(message = "Model ID è obbligatorio")
	private LookupElementDTOLong<ModelDTO> model;

	@NotBlank(message = "Document type è obbligatorio")
	private String documentType;

	private Long documentTemplateId;

	private String processKey;

	private LookupElementDTOLong<FolderDTO> folderDefault;

	private Boolean folderDefaultMandatory;

	private String description;

}
