package it.interzen.zencommonlibrary.dto.zenprocess;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProcessSubcategoryDTO extends TrackBasicChangesDTO implements HasID<Long> {
	Long id;
	String description;
	ProcessCategoryDTO processCategory;
}
