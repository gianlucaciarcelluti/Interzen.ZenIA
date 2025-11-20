package it.interzen.zencommonlibrary.dto.zenprotocollo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserDetailsDTO {
    private Long id;
    private String username;
    private String name;
    private String surname;
    private String email;
}
