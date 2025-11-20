package it.interzen.zencommonlibrary.dto.zenadmin;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author Gianluca Ciarcelluti
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class NotificationDTO {
    private String themeCode;
    private String title;
    private String description;
    private Integer notificationCount = 0;
    private Boolean featured = false;
    private Integer order = 0;
}