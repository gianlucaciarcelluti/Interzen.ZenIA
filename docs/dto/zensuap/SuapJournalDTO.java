package it.interzen.zencommonlibrary.dto.zensuap;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.slf4j.event.Level;

import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
public class SuapJournalDTO extends TrackBasicChangesDTO implements HasID<Long> {
    Long id;
    String cuiUuid;
    LocalDateTime timestamp;
    String description;
    InstanceStatusEnum status;
    DirectionEnum direction;
    Level level;
}
