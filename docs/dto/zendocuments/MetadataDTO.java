package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;


import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Data;

import java.util.List;

@Data
public class MetadataDTO implements HasID<Long>{
	private Long id;
		
	@NotNull
	String modelCode;
	
	@NotNull
	private Long objectId;
		
	@Enumerated(EnumType.STRING)
	@NotNull
	private MetadataTypeEnum objectType;

	// Elenca i metadati associati all'oggetto
	private List<MetadataValueDTO> metadata;
}
