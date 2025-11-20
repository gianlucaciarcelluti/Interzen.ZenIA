package it.interzen.zencommonlibrary.dto.zenprotocollo;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SpecialRegisterTypeDTO extends TrackBasicChangesDTO implements HasID<Long> {
    private Long id;
    
    @NotNull
    private String name;
    
    @NotNull
    private String registryCode;
}
