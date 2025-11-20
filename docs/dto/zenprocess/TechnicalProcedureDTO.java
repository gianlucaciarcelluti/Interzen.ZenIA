package it.interzen.zencommonlibrary.dto.zenprocess;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TechnicalProcedureDTO extends TrackBasicChangesDTO implements HasID<Long>{

	private Long id;
	private String name;
	private String description;
	private String overview;
	private String processId;
	private String processName;
	private AdministrativeProcedureDTO administrativeProcedure;

}
