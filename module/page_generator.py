import re
import module.file_handler as fh
import module.study_ as study


class HTMLSerializer:
    def __init__(self):
        pass

    def serialize_circuit(self, circuit):
        result = f"<h2>{circuit}</h2>"
        result += self.serialize_open_tag("ul")
        for part in circuit:
            result += self.serialize_open_tag("li")
            result += str(part)
            result += self.serialize_close_tag("li")
        result += self.serialize_close_tag("ul")
        return result

    def SerializeProductDescription(self, product):
        return product.GetName() + " (profit per sale: " + self.SerializeCurrency(product.GetProfitPerSale()) + ")\n"

    def SerializeTableOfSales(self, retailer):
        result = self.serialize_open_tag("table")
        # Header
        result += self.serialize_open_tag("tr")
        result += self.serialize_open_tag("th")
        result += "Product\n"
        result += self.serialize_close_tag("th")
        for monthNumber in range(1, 13):
            result += self.serialize_open_tag("th")
            result += self.GetMonthTrigramFromMonthNumber(monthNumber) + "\n"
            result += self.serialize_close_tag("th")
        result += self.serialize_close_tag("tr")
        # Sales
        for product in retailer.GetProducts():
            result += self.serialize_open_tag("tr")
            result += self.serialize_open_tag("td")
            result += product.GetName() + "\n"
            result += self.serialize_close_tag("td")
            for monthNumber in range(1, 13):
                result += self.serialize_open_tag("td")
                result += str(product.GetMonthlySales(monthNumber)) + "\n"
                result += self.serialize_close_tag("td")
            result += self.serialize_close_tag("tr")
        result += self.serialize_close_tag("table")
        return result

    def SerializeTableOfProfits(self, retailer):
        result = self.serialize_open_tag("table")
        # Header
        result += self.serialize_open_tag("tr")
        result += self.serialize_open_tag("th")
        result += "Product\n"
        result += self.serialize_close_tag("th")
        for monthNumber in range(1, 13):
            result += self.serialize_open_tag("th")
            result += self.GetMonthTrigramFromMonthNumber(monthNumber) + "\n"
            result += self.serialize_close_tag("th")
        result += self.serialize_open_tag("th")
        result += "Year\n"
        result += self.serialize_close_tag("th")
        result += self.serialize_close_tag("tr")
        # Profits
        for product in retailer.GetProducts():
            result += self.serialize_open_tag("tr")
            result += self.serialize_open_tag("td")
            result += product.GetName() + "\n"
            result += self.serialize_close_tag("td")
            for monthNumber in range(1, 13):
                result += self.serialize_open_tag("td")
                result += self.SerializeCurrency(product.ComputeMonthlyProfit(monthNumber)) + "\n"
                result += self.serialize_close_tag("td")
            result += self.serialize_open_tag("td")
            result += self.SerializeCurrency(product.ComputeYearlyProfit()) + "\n"
            result += self.serialize_close_tag("td")
            result += self.serialize_close_tag("tr")
        # Total
        result += self.serialize_open_tag("tr")
        result += self.serialize_open_tag("td")
        result += "Total\n"
        result += self.serialize_close_tag("td")
        for monthNumber in range(1, 13):
            result += self.serialize_open_tag("td")
            result += self.SerializeCurrency(retailer.ComputeMonthlyProfit(monthNumber))
            result += self.serialize_close_tag("td")
        result += self.serialize_open_tag("td")
        result += self.SerializeCurrency(retailer.ComputeYearlyProfit())
        result += self.serialize_close_tag("td")
        result += self.serialize_close_tag("tr")
        result += self.serialize_close_tag("table")
        return result

    @staticmethod
    def serialize_open_tag(name):
        return f"<{name}>"

    @staticmethod
    def serialize_close_tag(name):
        return f"</{name}>"

    @staticmethod
    def serialize_image(img_path):
        return f"<img src={img_path}>"


# 3. HTML Creator
# --------------

class HTMLCreator:
    def __init__(self):
        self.serializer = HTMLSerializer()
        self.study = study.Study()

    def ExportRetailerSalesAtHTMLFormat(self, retailer, templateFileName, targetFileName):
        try:
            templateFile = open(templateFileName, "r")
        except:
            sys.stderr.write('Unable to open file "%s"\n' % templateFileName)
            sys.stderr.flush()
            return 1
        try:
            targetFile = open(targetFileName, "w")
        except:
            sys.stderr.write('Unable to open file "%s"\n' % targetFileName)
            sys.stderr.flush()
            templateFile.close()
            return 1
        self.PrintReport(retailer, templateFile, targetFile)
        templateFile.close()
        targetFile.flush()
        targetFile.close()
        return 0

    def PrintImg(self, circuit):
        self.study.example_study(circuit)

    def PrintReport(self, retailer, templateFile, targetFile):
        for line in templateFile:
            line = line.rstrip()
            if re.search(r'__PRODUCTS__', line):
                line = re.sub(r'__PRODUCTS__', self.serializer.SerializeListOfProducts(retailer), line)
            elif re.search(r'__SALES__', line):
                line = re.sub(r'__SALES__', self.serializer.SerializeTableOfSales(retailer), line)
            elif re.search(r'__PROFITS__', line):
                line = re.sub(r'__PROFITS__', self.serializer.SerializeTableOfProfits(retailer), line)
            targetFile.write(line + "\n")

'''
class PageGenerator:
    def __init__(self, template_file, target_file, **kwargs):
        self._template_file = template_file
        self._target_file = target_file
        self.study_serializer = StudyHTMLSerializer()
        self.render_study(self.template_file, self.target_file)

    @property
    def template_file(self):
        return self._template_file

    @property
    def target_file(self):
        return self._target_file

    def render_study(self, circuit, template_file, target_file):
        with fh.File(template_file, "r") as template:
            with fh.File(target_file, "w") as target:
                for line in template:
                    line = self.HTML_replacement(circuit, line)
                    target.write(line + '\n')

    def serialize_circuit(self, circuit) -> str:

        pass

    def HTML_replacement(self, circuit, line: str):
        line = line.rstrip()
        # Methods to be called to replace placeholder in template with some value.
        methods = {r'__Circuit__': lambda: re.sub(r'__Circuit__',
                                                  self.study_serializer.serialize_circuit(circuit), line),
                   r'__base_study__': lambda: re.sub(r'__base_study__', self.study_serializer
                                                     .serialize_circuit(circuit), line)}
        for key in methods:
            if re.search(key, line):
                return methods[key]
        return line
'''
