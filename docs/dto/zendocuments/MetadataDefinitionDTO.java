package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;
import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Data;

@Data
public class MetadataDefinitionDTO implements HasID<Long>{
	private Long id;
		
	@NotNull
	private String code;
	
	@NotNull
	private String name;
	
	private String description;
	
	@NotNull
	@Enumerated(EnumType.STRING)
	MetadataDefTypeEnum type;
		
	String query;
		
	@NotNull
	Boolean active = true;
}
