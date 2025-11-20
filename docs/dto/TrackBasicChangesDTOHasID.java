package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TrackBasicChangesDTOHasID<PK> extends TrackBasicChangesDTO implements HasID<PK>{
	protected PK id;
}
