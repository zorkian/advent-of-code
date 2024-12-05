from .day import Day


class Day5(Day):
    def __init__(self, use_test_data=False):
        self.rules = {}
        self.lists = []
        super().__init__(day_number=5, use_test_data=use_test_data)

    def parse_input(self):
        sections = "\n".join(self.input_data).strip().split("\n\n")

        if len(sections) == 2:
            rules_section, lists_section = sections

            for line in rules_section.splitlines():
                before, after = line.split('|')
                self.rules.setdefault(before.strip(), []).append(after.strip())

            for line in lists_section.split('\n'):
                self.lists.append([page.strip() for page in line.split(',') if page.strip()])

    def find_valid_lists(self):
        valid_lists = []
        invalid_lists = []
        for lst in self.lists:
            valid = True
            for i in range(len(lst)):
                current_page = lst[i]
                if current_page in self.rules:
                    for required_page in self.rules[current_page]:
                        if required_page in lst and lst.index(required_page) < i:
                            valid = False
                            break
            if valid:
                valid_lists.append(lst)
            else:
                invalid_lists.append(lst)
        return valid_lists, invalid_lists

    def solve_part_one(self):
        valid_lists, _  = self.find_valid_lists()
        middle_sum = sum(int(lst[len(lst) // 2]) for lst in valid_lists if len(lst) > 0 and lst[len(lst) // 2].isdigit())
        return middle_sum

    def solve_part_two(self):
        _, invalid_lists = self.find_valid_lists()
        adjusted_lists = []

        for lst in invalid_lists:
            adjusted_list = lst.copy()
            changed = True
            while changed:
                changed = False
                for i in range(len(adjusted_list)):
                    current_page = adjusted_list[i]
                    if current_page in self.rules:
                        for required_page in self.rules[current_page]:
                            if required_page in adjusted_list and adjusted_list.index(required_page) < i:
                                adjusted_list.remove(current_page)
                                adjusted_list.insert(adjusted_list.index(required_page), current_page)
                                changed = True
                                break

            adjusted_lists.append(adjusted_list)

        middle_sum = sum(int(adjusted_list[len(adjusted_list) // 2]) for adjusted_list in adjusted_lists if adjusted_list and adjusted_list[len(adjusted_list) // 2].isdigit())
        return middle_sum
