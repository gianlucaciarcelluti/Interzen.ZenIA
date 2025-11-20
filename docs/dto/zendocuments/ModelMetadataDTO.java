package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Data;

import java.util.List;

@Data
public class ModelMetadataDTO implements HasID<Long>{
	private Long id;
		
	@NotNull
	String modelCode;
	
	@NotNull
	String metadataCode;
	
	Boolean active = true;

	String label;

	Integer position = 0;
	
	Boolean mandatory = false;
	
	Boolean unique = false;
	
	String defaultValue;
		
	@Enumerated(EnumType.STRING)
    LegaArchiveTypeEnum legalArchiveType;

	@Enumerated(EnumType.STRING)
	MetadataDefTypeEnum type;

    Boolean readonly = false;

	// Valori di lookup
	private List<LookupDTO> lookupValues;
}
